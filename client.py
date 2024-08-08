import socket

def send_request(client_name, command):  
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 9999))

    
    data = f"{client_name}|{command}"
    print(f"CHECK : {data}")
    client.send(data.encode('utf-8'))
    
    response = client.recv(4096).decode('utf-8')
    client.close()
    print(response)


if __name__ == "__main__":
    
    client_name = input("กรุณากรอกชื่อของคุณ: ")

    print("คำสั่งที่ใช้งานได้ : ")
    print("จอง วันที่/เดือน เวลา (ex. 00/00 00:00) - เพื่อทำการจองเวลาที่ต้องการเข้าใช้บริการ ")
    print("ยกเลิก วันที่/เดือน เวลา (ex. 00/00 00:00) - เพื่อยกเลิกคำสั่งจอง")
    print("ตาราง - เพื่อเช็ควัน เวลา ที่ต้องการเข้าใช้บริการ")
    print("EXIT - เพื่อออกจากระบบ")

    while True:
        print(f"CLIENT_NAME : {client_name}")
        
        command = input("กรุณาระบุคำสั่งที่ต้องการใช้งาน : ")
        
        if command.upper() == "EXIT":
            break
        
        send_request(client_name, command)
