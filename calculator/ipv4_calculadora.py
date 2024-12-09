# ipv4_calculato.py
import ipaddress

def get_ip_class(ip):
    first_octet = int(ip.split('.')[0])
    if 1 <= first_octet <= 126:
        return "Clase A"
    elif 128 <= first_octet <= 191:
        return "Clase B"
    elif 192 <= first_octet <= 223:
        return "Clase C"
    else:
        return "Reservada o Pública"

def get_ip_type(ip):
    ip_obj = ipaddress.IPv4Address(ip)
    return "Privada" if ip_obj.is_private else "Pública"

def ipv4_calculator():
    print("Calculadora IPv4")
    
    while True:
        try:
            ip = input("Ingrese una dirección IPv4: ")
            ipaddress.IPv4Address(ip)  # Valida que sea una IP correcta
            break
        except ValueError:
            print("Dirección IP no válida, por favor intente de nuevo.")

    while True:
        try:
            prefix = int(input("Ingrese el prefijo de subred (ejemplo, /24): ").strip("/"))
            if 0 <= prefix <= 32:
                break
            else:
                print("Prefijo no válido. Debe estar entre 0 y 32.")
        except ValueError:
            print("Entrada no válida. Por favor, ingrese un número entero.")

    network = ipaddress.IPv4Network(f"{ip}/{prefix}", strict=False)

    print(f"\nDirección IPv4 ingresada: {ip}")
    print(f"Dirección de red: {network.network_address}")
    print(f"Dirección de broadcast: {network.broadcast_address}")
    print(f"Máscara de subred: {network.netmask}")
    print(f"Número total de hosts: {network.num_addresses}")
    print(f"Número de hosts utilizables: {network.num_addresses - 2}")
    print(f"Rango de IPs utilizables: {network.network_address + 1} - {network.broadcast_address - 1}")
    print(f"Notación CIDR: /{prefix}")
    print(f"Clase de IP: {get_ip_class(str(network.network_address))}")
    print(f"Tipo de IP: {get_ip_type(str(network.network_address))}")

if __name__ == "__main__":
    ipv4_calculator()
