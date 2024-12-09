# flsm_calculatorr.py
import ipaddress
import math

def calculate_flsm(ip, prefix, num_subnets, hosts_per_subnet):
    """Calcula las subredes FLSM."""
    network = ipaddress.IPv4Network(f"{ip}/{prefix}", strict=False)

    # Asegúrate de que cada subred tenga suficientes direcciones para los hosts + 2
    required_hosts = hosts_per_subnet + 2
    new_prefix = 32 - math.ceil(math.log2(required_hosts))

    # Generar las subredes según el número de subredes solicitado
    subnets = list(network.subnets(new_prefix=new_prefix))[:num_subnets]

    return [
        {
            "Subnet Number": i + 1,
            "Network Address": str(subnet.network_address),
            "Broadcast Address": str(subnet.broadcast_address),
            "Total Hosts": subnet.num_addresses,
            "Usable Hosts": subnet.num_addresses - 2,
            "Usable Host IP Range": f"{subnet.network_address + 1} - {subnet.broadcast_address - 1}",
            "Subnet Mask": str(subnet.netmask),
            "CIDR Notation": f"/{new_prefix}",
            "step_by_step": generate_flsm_explanation(subnet.network_address, new_prefix, hosts_per_subnet)
        }
        for i, subnet in enumerate(subnets)
    ]

def generate_flsm_explanation(network_address, new_prefix, hosts_per_subnet):
    """Genera la explicación paso a paso."""
    total_hosts = hosts_per_subnet + 2  # Incluye red y broadcast
    bits_for_hosts = math.ceil(math.log2(total_hosts))  # Cálculo correcto

    return (
        "\nExplicación paso a paso:\n"
        f"1. Dirección IP inicial: {network_address}\n"
        f"2. Para {hosts_per_subnet} hosts, se necesitan {total_hosts} direcciones "
        f"(incluyendo IP de red y broadcast).\n"
        f"3. El número de bits necesarios para cubrir {total_hosts} hosts es: "
        f"{bits_for_hosts} bits para hosts.\n"
        f"4. El nuevo prefijo será /{new_prefix}.\n"
        f"5. La máscara de subred asociada es: {ipaddress.IPv4Network(f'0.0.0.0/{new_prefix}').netmask}.\n"
    )

def print_flsm_report(subnets):
    """Imprime el reporte para todas las subredes generadas."""
    print("\nFLSM Calculation Report:")
    print("-" * 50)
    for subnet in subnets:
        for key, value in subnet.items():
            if key != "step_by_step":
                print(f"{key}: {value}")
        print(subnet["step_by_step"])
        print("-" * 50)

def main():
    """Función principal para la calculadora FLSM."""
    print("Calculadora FLSM")

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

    while True:
        try:
            hosts_per_subnet = int(input("Por favor, introduzca el número de hosts por subred: "))
            if hosts_per_subnet > 0:
                break
            else:
                print("El número de hosts debe ser mayor que 0.")
        except ValueError:
            print("Entrada no válida. Por favor, ingrese un número entero.")

    subnets = calculate_flsm(ip, prefix, num_subnets, hosts_per_subnet)
    print_flsm_report(subnets)

if __name__ == "__main__":
    main()
