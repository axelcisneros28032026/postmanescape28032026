import json
import socket
import threading

from PySide6.QtCore import QObject, Signal, QThread


# ──────────────────────────────────────────────────────────────────────────────
# Hilo de lectura continua (compartido por servidor y cliente)
# ──────────────────────────────────────────────────────────────────────────────
class _ReaderThread(QThread):
    """Lee paquetes JSON de un socket y emite la señal 'received'."""

    received = Signal(dict)
    disconnected = Signal()

    def __init__(self, sock: socket.socket):
        super().__init__()
        self._sock = sock
        self._running = True

    def run(self):
        buffer = ""
        while self._running:
            try:
                data = self._sock.recv(4096)
                if not data:
                    break
                buffer += data.decode("utf-8", errors="replace")
                # Los paquetes están separados por '\n'
                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    line = line.strip()
                    if line:
                        try:
                            self.received.emit(json.loads(line))
                        except json.JSONDecodeError:
                            pass
            except OSError:
                break
        self.disconnected.emit()

    def stop(self):
        self._running = False
        try:
            self._sock.shutdown(socket.SHUT_RDWR)
        except OSError:
            pass


# ──────────────────────────────────────────────────────────────────────────────
# Servidor  (Enemy)
# ──────────────────────────────────────────────────────────────────────────────
class GameServer(QObject):
    """
    Escucha en *port* y acepta UN cliente.
    Señales:
        client_connected()          → llegó el cliente
        received(dict)              → paquete recibido del cliente
        disconnected()              → cliente se desconectó
    """

    client_connected = Signal()
    received = Signal(dict)
    disconnected = Signal()

    def __init__(self, port: int = 25565):
        super().__init__()
        self._port = port
        self._server_sock: socket.socket | None = None
        self._client_sock: socket.socket | None = None
        self._reader: _ReaderThread | None = None
        self._accept_thread: threading.Thread | None = None

    # ── API pública ────────────────────────────────────────────────────────────
    def start(self):
        """Abre el servidor y espera al cliente en un hilo de fondo."""
        self._server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._server_sock.bind(("0.0.0.0", self._port))
        self._server_sock.listen(1)
        self._accept_thread = threading.Thread(target=self._accept, daemon=True)
        self._accept_thread.start()

    def send(self, data: dict):
        """Envía un paquete JSON al cliente conectado."""
        if self._client_sock:
            try:
                self._client_sock.sendall((json.dumps(data) + "\n").encode("utf-8"))
            except OSError:
                pass

    def stop(self):
        if self._reader:
            self._reader.stop()
        try:
            if self._server_sock:
                self._server_sock.close()
        except OSError:
            pass

    # ── Interno ────────────────────────────────────────────────────────────────
    def _accept(self):
        try:
            self._client_sock, addr = self._server_sock.accept()
            print(f"[Servidor] Cliente conectado desde {addr}")
            self._reader = _ReaderThread(self._client_sock)
            self._reader.received.connect(self.received)
            self._reader.disconnected.connect(self.disconnected)
            self._reader.start()
            self.client_connected.emit()
        except OSError:
            pass


# ──────────────────────────────────────────────────────────────────────────────
# Cliente  (Player)
# ──────────────────────────────────────────────────────────────────────────────
class GameClient(QObject):
    """
    Se conecta a *host*:*port*.
    Señales:
        connected()                 → conexión exitosa
        received(dict)              → paquete recibido del servidor
        disconnected()              → servidor se desconectó
        connection_failed(str)      → no se pudo conectar
    """

    connected = Signal()
    received = Signal(dict)
    disconnected = Signal()
    connection_failed = Signal(str)

    def __init__(self, host: str = "127.0.0.1", port: int = 25565):
        super().__init__()
        self._host = host
        self._port = port
        self._sock: socket.socket | None = None
        self._reader: _ReaderThread | None = None

    # ── API pública ────────────────────────────────────────────────────────────
    def connect_to_server(self):
        """Intenta conectarse en un hilo de fondo."""
        t = threading.Thread(target=self._connect, daemon=True)
        t.start()

    def send(self, data: dict):
        """Envía un paquete JSON al servidor."""
        if self._sock:
            try:
                self._sock.sendall((json.dumps(data) + "\n").encode("utf-8"))
            except OSError:
                pass

    def stop(self):
        if self._reader:
            self._reader.stop()
        try:
            if self._sock:
                self._sock.close()
        except OSError:
            pass

    # ── Interno ────────────────────────────────────────────────────────────────
    def _connect(self):
        try:
            self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._sock.settimeout(5)
            self._sock.connect((self._host, self._port))
            self._sock.settimeout(None)
            self._reader = _ReaderThread(self._sock)
            self._reader.received.connect(self.received)
            self._reader.disconnected.connect(self.disconnected)
            self._reader.start()
            self.connected.emit()
        except (OSError, TimeoutError) as e:
            self.connection_failed.emit(str(e))