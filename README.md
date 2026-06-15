# TCP Multithreaded Chat Application

A real-time, concurrent client-server chat application built using Python's standard networking stack.

## Features
* **Multi-threaded Architecture:** Implements a multi-threaded server model using the `threading` library, allowing multiple distinct clients to communicate concurrently without blocking the core socket event loop.
* **TCP/IP Protocol:** Utilizes streaming internet sockets (`SOCK_STREAM`) to ensure reliable, connection-oriented packet delivery.
* **Dynamic State Management:** Automatically handles user authentication via custom nicknames, broadcasts room-wide notifications, and gracefully manages unexpected client disconnections.
