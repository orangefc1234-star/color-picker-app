from pyscript import document, window

# ตัวแปรสำหรับเก็บรายชื่อและคะแนน (List of Dictionaries)
students_data = []

def update_dashboard():
    # หากไม่มีข้อมูลให้รีเซ็ตหน้าจอเป็น 0
    if not students_data:
        document.getElementById("count").innerText = "0"
        document.getElementById("avg").innerText = "0.00"
        document.getElementById("max").innerText = "0"
        document.getElementById("min").innerText = "0"
        return

    # ดึงเฉพาะตัวเลขคะแนนออกมาคำนวณ
    scores = [s["score"] for s in students_data]
    
    total_students = len(scores)
    avg_score = sum(scores) / total_students
    max_score = max(scores)
    min_score = min(scores)

    # แสดงผลบนแดชบอร์ด
    document.getElementById("count").innerText = str(total_students)
    document.getElementById("avg").innerText = f"{avg_score:.2f}"
    document.getElementById("max").innerText = str(max_score)
    document.getElementById("min").innerText = str(min_score)

def update_table():
    tbody = document.getElementById("table-body")
    tbody.innerHTML = "" 
    
    # วนลูปสร้างแถวข้อมูลในตาราง
    for index, student in enumerate(students_data):
        score = student["score"]
        # กำหนดเงื่อนไขผ่านเกณฑ์ที่ 50 คะแนน
        status = "✅ ผ่าน" if score >= 50 else "❌ ไม่ผ่าน"
        color = "green" if score >= 50 else "red"
        
        row_html = f"""
        <tr>
            <td>{index + 1}</td>
            <td>{student["name"]}</td>
            <td>{score}</td>
            <td style="color: {color}; font-weight: bold;">{status}</td>
        </tr>
        """
        tbody.innerHTML += row_html

def add_score(event):
    name_input = document.getElementById("student-name")
    score_input = document.getElementById("student-score")
    
    name = name_input.value.strip()
    score_text = score_input.value.strip()
    
    if not name or not score_text:
        window.alert("กรุณากรอกชื่อและคะแนนให้ครบถ้วน")
        return
        
    try:
        score = float(score_text)
        if score < 0 or score > 100:
            window.alert("กรุณากรอกคะแนนระหว่าง 0 - 100")
            return
            
        students_data.append({"name": name, "score": score})
        
        # ล้างช่องข้อความหลังบันทึกเสร็จ
        name_input.value = ""
        score_input.value = ""
        
        # สั่งรีเฟรชข้อมูล
        update_table()
        update_dashboard()
        
    except ValueError:
        window.alert("คะแนนต้องเป็นตัวเลขเท่านั้น")

def clear_data(event):
    if window.confirm("ต้องการลบข้อมูลทั้งหมดใช่หรือไม่?"):
        students_data.clear()
        update_table()
        update_dashboard()
