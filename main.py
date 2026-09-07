from pyscript import document, window
from pyodide.ffi import to_js
import asyncio

video = document.getElementById("camera-feed")
canvas = document.getElementById("snapshot-canvas")
ctx = canvas.getContext("2d")

rgb_text = document.getElementById("rgb-value")
hex_text = document.getElementById("hex-value")
color_preview = document.getElementById("color-preview")

async def start_video(event):
    try:
        # ขอสิทธิ์เข้าถึงกล้อง (บังคับเปิดกล้องหลังถ้าใช้งานบนมือถือ)
        constraints = to_js({"video": {"facingMode": "environment"}})
        
        # เรียกใช้ Web API ของเบราว์เซอร์
        stream = await window.navigator.mediaDevices.getUserMedia(constraints)
        video.srcObject = stream
    except Exception as e:
        window.alert("ไม่สามารถเปิดกล้องได้ โปรดตรวจสอบการอนุญาตใช้งานกล้องบนเบราว์เซอร์ของคุณ")

def pick_color(event):
    # ตรวจสอบว่ากล้องเปิดและส่งภาพมาแล้วหรือไม่
    if not video.videoWidth:
        return

    # 1. กำหนดขนาด Canvas ให้เท่ากับวิดีโอ
    canvas.width = video.videoWidth
    canvas.height = video.videoHeight

    # 2. วาดเฟรมภาพปัจจุบันจากวิดีโอลงใน Canvas แบบซ่อน
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height)

    # 3. คำนวณพิกัดแกน X, Y ที่ถูกคลิก โดยเทียบสัดส่วนหน้าจอกับขนาดวิดีโอจริง
    rect = video.getBoundingClientRect()
    scale_x = canvas.width / rect.width
    scale_y = canvas.height / rect.height
    
    x = (event.clientX - rect.left) * scale_x
    y = (event.clientY - rect.top) * scale_y

    # 4. ดึงข้อมูลพิกเซล (Red, Green, Blue, Alpha) ในตำแหน่ง 1x1 พิกเซล
    pixel = ctx.getImageData(x, y, 1, 1).data
    r, g, b = pixel[0], pixel[1], pixel[2]
    
    # 5. แปลงค่าสีเป็นระบบฐาน 16 (HEX Code)
    hex_code = f"#{r:02x}{g:02x}{b:02x}".upper()
    
    # 6. อัปเดตผลลัพธ์ลงบนหน้าเว็บ
    rgb_text.innerText = f"{r}, {g}, {b}"
    hex_text.innerText = hex_code
    color_preview.style.backgroundColor = hex_code
