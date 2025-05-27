import os
from azure.servicebus import ServiceBusClient, ServiceBusMessage, TransportType

# Configuración de Azure Service Bus (usa WebSocket para evitar bloqueos de red)
CONNECTION_STR = "Endpoint=sb://loped2.servicebus.windows.net/;SharedAccessKeyName=admin;SharedAccessKey=glbdHipkra6QP22ZcHAVeW18Yn0OFRhMK+ASbPZDxMU="
QUEUE_NAME = "loped2"

def enviar_mensaje(texto):
    """Envía un mensaje simple al Service Bus."""
    servicebus_client = ServiceBusClient.from_connection_string(
        conn_str=CONNECTION_STR,
        transport_type=TransportType.AmqpOverWebsocket  # ✅ USAMOS WEBSOCKETS
    )
    
    with servicebus_client:
        sender = servicebus_client.get_queue_sender(queue_name=QUEUE_NAME)
        with sender:
            mensaje = ServiceBusMessage(texto)
            sender.send_messages(mensaje)
            print(f"✅ Mensaje enviado: '{texto}'")

def ver_mensajes():
    """Recibe y elimina los mensajes de la cola."""
    servicebus_client = ServiceBusClient.from_connection_string(
        conn_str=CONNECTION_STR,
        transport_type=TransportType.AmqpOverWebsocket # ✅ TAMBIÉN AQUÍ
    )

    with servicebus_client:
        receiver = servicebus_client.get_queue_receiver(queue_name=QUEUE_NAME, max_wait_time=5)
        with receiver:
            for mensaje in receiver:
                print("📨 Mensaje recibido:", b"".join(mensaje.body).decode("utf-8"))
                receiver.complete_message(mensaje)

if __name__ == "__main__":
    opcion = input("¿Qué deseas hacer? (1=Enviar mensaje, 2=Ver mensajes): ").strip()
    
    if opcion == "1":
        texto = input("Introduce una palabra o mensaje para enviar: ").strip()
        if texto:
            enviar_mensaje(texto)
        else:
            print("❗ Entrada vacía.")
    
    elif opcion == "2":
        ver_mensajes()
    
    else:
        print("❌ Opción no válida.")

