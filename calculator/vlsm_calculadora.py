import ipaddress
import math

# Diccionario que contiene la relación entre el prefijo CIDR y su máscara de subred y máscara comodín
CIDR_INFO = {
    32: ("255.255.255.255", "0.0.0.0", 1, 1),
    31: ("255.255.255.254", "0.0.0.1", 2, 2),
    30: ("255.255.255.252", "0.0.0.3", 4, 2),
    29: ("255.255.255.248", "0.0.0.7", 8, 6),
    28: ("255.255.255.240", "0.0.0.15", 16, 14),
    27: ("255.255.255.224", "0.0.0.31", 32, 30),
    26: ("255.255.255.192", "0.0.0.63", 64, 62),
    25: ("255.255.255.128", "0.0.0.127", 128, 126),
    24: ("255.255.255.0", "0.0.0.255", 256, 254),
    23: ("255.255.254.0", "0.0.1.255", 512, 510),
    22: ("255.255.252.0", "0.0.3.255", 1024, 1022),
    21: ("255.255.248.0", "0.0.7.255", 2048, 2046),
    20: ("255.255.240.0", "0.0.15.255", 4096, 4094),
    19: ("255.255.224.0", "0.0.31.255", 8192, 8190),
    18: ("255.255.192.0", "0.0.63.255", 16384, 16382),
    17: ("255.255.128.0", "0.0.127.255", 32768, 32766),
    16: ("255.255.0.0", "0.0.255.255", 65536, 65534),
    15: ("255.254.0.0", "0.1.255.255", 131072, 131070),
    14: ("255.252.0.0", "0.3.255.255", 262144, 262142),
    13: ("255.248.0.0", "0.7.255.255", 524288, 524286),
    12: ("255.240.0.0", "0.15.255.255", 1048576, 1048574),
    11: ("255.224.0.0", "0.31.255.255", 2097152, 2097150),
    10: ("255.192.0.0", "0.63.255.255", 4194304, 4194302),
    9: ("255.128.0.0", "0.127.255.255", 8388608, 8388606),
    8: ("255.0.0.0", "0.255.255.255", 16777216, 16777214),
    7: ("254.0.0.0", "1.255.255.255", 33554432, 33554430),
    6: ("252.0.0.0", "3.255.255.255", 67108864, 67108862),
    5: ("248.0.0.0", "7.255.255.255", 134217728, 134217726),
    4: ("240.0.0.0", "15.255.255.255", 268435456, 268435454),
    3: ("224.0.0.0", "31.255.255.255", 536870912, 536870910),
    2: ("192.0.0.0", "63.255.255.255", 1073741824, 1073741822),
    1: ("128.0.0.0", "127.255.255.255", 2147483648, 2147483646),
    0: ("0.0.0.0", "255.255.255.255", 4294967296, 4294967294),
}

def get_ip_class(ip):
    first_octet = int(ip.split('.')[0])
    if 1 <= first_octet <= 126:
        return "Clase A", "Clase A cubre direcciones desde 1.0.0.0 hasta 126.255.255.255 (IP privadas: 10.0.0.0/8)."
    elif 128 <= first_octet <= 191:
        return "Clase B", "Clase B cubre direcciones desde 128.0.0.0 hasta 191.255.255.255 (IP privadas: 172.16.0.0/12)."
    elif 192 <= first_octet <= 223:
        return "Clase C", "Clase C cubre direcciones desde 192.0.0.0 hasta 223.255.255.255 (IP privadas: 192.168.0.0/16)."
    else:
        return "Reservada o Pública", "Esta dirección no pertenece a las clases A, B o C."

def get_ip_type(ip):
    ip_obj = ipaddress.IPv4Address(ip)
    return "Privada" if ip_obj.is_private else "Pública"

def calculate_vlsm(ip, prefix, subnets_info):
    network = ipaddress.IPv4Network(f"{ip}/{prefix}", strict=False)
    current_address = network.network_address
    subnets = []

    sorted_subnets = sorted(subnets_info.items(), key=lambda x: x[1], reverse=True)

    for subnet_name, hosts in sorted_subnets:
        required_hosts = hosts + 2
        new_prefix = 32 - math.ceil(math.log2(required_hosts))
        subnet_mask, wildcard_mask, total_ips, usable_ips = CIDR_INFO[new_prefix]
        subnet = ipaddress.IPv4Network(f"{current_address}/{new_prefix}", strict=False)

        ip_class, class_explanation = get_ip_class(str(current_address))

        subnet_data = {
            "IP Address": str(current_address),
            "Network Address": str(subnet.network_address),
            "Broadcast Address": str(subnet.broadcast_address),
            "Total Number of Hosts": subnet.num_addresses,
            "Number of Usable Hosts": subnet.num_addresses - 2,
            "Usable Host IP Range": f"{subnet.network_address + 1} - {subnet.broadcast_address - 1}",
            "Subnet Mask": subnet_mask,
            "Wildcard Mask": wildcard_mask,
            "IP Class": ip_class,
            "Class Explanation": class_explanation,
            "CIDR Notation": f"/{new_prefix}",
            "IP Type": get_ip_type(str(current_address)),
            "name": subnet_name,
            "step_by_step": generate_step_by_step_explanation(current_address, new_prefix, hosts, required_hosts)  # Añadir paso a paso
        }
        subnets.append(subnet_data)
        current_address = subnet.broadcast_address + 1

    return subnets

def generate_step_by_step_explanation(ip, new_prefix, hosts, required_hosts):
    explanation = "\nExplicación paso a paso:\n"
    explanation += f"1. Dirección IP inicial: {ip}\n"
    explanation += f"2. Para {hosts} hosts, se necesitan {required_hosts} direcciones (incluyendo IP de red y broadcast).\n"
    explanation += f"3. El número de bits necesarios para cubrir {required_hosts} hosts es {32 - new_prefix} bits para los hosts.\n"
    explanation += f"4. El nuevo prefijo será /{new_prefix}, lo que significa que {32 - new_prefix} bits se usan para las direcciones de host.\n"
    explanation += f"5. La máscara de subred asociada es: {CIDR_INFO[new_prefix][0]}.\n"
    explanation += f"6. La cantidad total de direcciones en esta subred es {2 ** (32 - new_prefix)} direcciones.\n"
    explanation += f"7. El rango de direcciones IP utilizables va desde {ip} hasta el broadcast menos una unidad.\n"
    return explanation

def print_report(subnets):
    print("\nSubnet Calculation Report:")
    print("-" * 50)
    for subnet in subnets:
        print(f"IP Address: {subnet['IP Address']}")
        print(f"Network Address: {subnet['Network Address']}")
        print(f"Broadcast Address: {subnet['Broadcast Address']}")
        print(f"Total Number of Hosts: {subnet['Total Number of Hosts']}")
        print(f"Number of Usable Hosts: {subnet['Number of Usable Hosts']}")
        print(f"Usable Host IP Range: {subnet['Usable Host IP Range']}")
        print(f"Subnet Mask: {subnet['Subnet Mask']}")
        print(f"Wildcard Mask: {subnet['Wildcard Mask']}")
        print(f"IP Class: {subnet['IP Class']}")
        print(f"Explicación de la clase: {subnet['Class Explanation']}")
        print(f"CIDR Notation: {subnet['CIDR Notation']}")
        print(f"IP Type: {subnet['IP Type']}")
        print(f"Subnet Name: {subnet['name']}")
        print(subnet['step_by_step'])  # Imprimir paso a paso
        print("-" * 50)

def main():
    print("Calculadora VLSM")

    while True:
        try:
            ip = input("Por favor, introduzca la dirección IPv4 de la red (e.g. 192.168.1.0): ")
            ipaddress.IPv4Address(ip)  # Valida la IP
            break
        except ValueError:
            print("Dirección IP no válida. Por favor, intente de nuevo.")

    while True:
        try:
            prefix = int(input("Por favor, introduzca el prefijo de subred (e.g. /24): ").strip("/"))
            if 0 <= prefix <= 32:
                break
            else:
                print("Prefijo no válido. Debe estar entre 0 y 32.")
        except ValueError:
            print("Entrada no válida. Por favor, ingrese un número entero.")

    while True:
        try:
            num_subnets = int(input("Por favor, introduzca el número de subredes: "))
            if num_subnets > 0:
                break
            else:
                print("El número de subredes debe ser mayor que 0.")
        except ValueError:
            print("Entrada no válida. Por favor, ingrese un número entero.")

    subnets_info = {}
    for _ in range(num_subnets):
        subnet_name = input("Nombre de la subred: ")
        while True:
            try:
                hosts = int(input(f"Cantidad de hosts para {subnet_name}: "))
                if hosts > 0:
                    subnets_info[subnet_name] = hosts
                    break
                else:
                    print("El número de hosts debe ser mayor que 0.")
            except ValueError:
                print("Entrada no válida. Por favor, ingrese un número entero.")

    subnets = calculate_vlsm(ip, prefix, subnets_info)
    print_report(subnets)

if __name__ == "__main__":
    main()
