class ComputerManager:
    def __init__(self):
        self.computers = {}

    def add_computer(self, mac_address):
            self.computers[mac_address] = True
            print("Computer added successfully.")

    def stop_computer(self, mac_address):
            self.computers[mac_address] = False
            print("Computer stop successfully.")

    def remove_computer(self, mac_address):
            del self.computers[mac_address]
            print("Computer removed successfully.")

    def view_computers(self):
        if not self.computers:
            print("No computers available.")
        else:
            for mac, status in self.computers.items():
                status_str = "On" if status else "Off"
                print(f"MAC: {mac}, Status: {status_str}")

    def chek_status(self,mac_address):
        return self.computers[mac_address]


status = ComputerManager()

