import socket
import threading


appointments = {}


def handle_client(client_socket):
    global appointments
    try:
        while True:
            
            data = client_socket.recv(1024).decode('utf-8')
            print(f"DATA : {data}")
            if not data:
                break
            
            
            client_name, request = data.split('|', 1)
            command, *args = request.split()

            print(f"CLIENT_NAME : {client_name}")
            print(f"REQUEST : {request}")

            if command == 'จอง':
                if len(args) != 2:
                    response = "300 Fail การจองผิดพลาด - กรุณาพิมพ์วันที่เวลาที่ต้องการจองตามรูปแบบที่กำหนด"
                else:
                    date, time_slot = args
                    appointment_key = f"{date} {time_slot}"
                    if appointment_key in appointments:
                        response = "202 Unavailable เวลาที่ต้องการจองถูกจองแล้ว กรุณาเลือกเวลาอื่น"
                    else:
                        appointments[appointment_key] = f'จองโดย {client_name}'
                        response = f"200 OK จองเวลาเรียบร้อยสำหรับ {appointment_key}\n ชื่อลูกค้า {client_name}\n กรุณาแสดงข้อความยืนยันนี้เมื่อถึงเวลานัด ขอบคุณที่ใช้บริการ see you soon <3"
                        print("\n".join(f"{slot}: {status}" for slot, status in appointments.items()))

            elif command == 'ยกเลิก':
                if len(args) != 2:
                    response = "300 Fail ไม่สามารถยกเลิกได้ - กรุณาพิมพ์วันที่เวลาที่ต้องการจองตามรูปแบบที่กำหนด"
                else:
                    date, time_slot = args
                    appointment_key = f"{date} {time_slot}"
                    if appointment_key in appointments and appointments[appointment_key] == f'จองโดย {client_name}':
                        del appointments[appointment_key]
                        response = f"200 OK คำสั่งจองของคุณถูกยกเลิกสำหรับ {appointment_key}!"
                    else:
                        response = "202 Unavailable ไม่มีคำสั่งจองที่สามารถยกเลิกได้ในช่วงเวลาที่ระบุ หรือคุณอาจจะไม่ได้เป็นผู้สั่งจองในเวลาที่ระบุ\n กรุณาระบุวันที่และเวลาที่ต้องการยกเลิกใหม่"
        
            elif command == 'ตาราง':
                if appointments:
                    response = "\n".join(f"{slot}: {status}" for slot, status in appointments.items())
                else:
                    response = "404 Not Found คิวว่าง ท่านสามารถระบุวันเวลาที่ต้องการจองตามรูปแบบที่กำหนดได้เลย"
        
            else:
                response = "300 Fail การจองผิดพลาด กรุณาพิมพ์คำสั่งตามรูปแบบที่กำหนด"
        
            client_socket.send(response.encode('utf-8'))
    
    except:
        print("เกิดข้อผิดพลาดในการรับข้อมูลจากลูกค้า")
    finally:
        client_socket.close()


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 9999))
    server.listen(5)
    print("Server listening on port 9999")

    while True:
        client_socket, addr = server.accept()
        print(f"Accepted connection from {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    start_server()
