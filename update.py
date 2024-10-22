import os
import subprocess

# --------------------------------------------------------------------------- #
# We execute Python scripts

script_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "scripts")

talk_script_path = os.path.join(script_path, "generate_talk.py")
pub_script_path = os.path.join(script_path, "generate_publication.py")
student_script_path = os.path.join(script_path, "generate_student.py")
position_script_path = os.path.join(script_path, "generate_position.py")

print(f"python {talk_script_path}")
subprocess.run(["python", talk_script_path])
print(f"python {pub_script_path}")
subprocess.run(["python", pub_script_path])
print(f"python {student_script_path}")
subprocess.run(["python", student_script_path])
print(f"python {position_script_path}")
subprocess.run(["python", position_script_path])
