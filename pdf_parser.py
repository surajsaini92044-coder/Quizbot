import fitz
import re

def extract_quiz_from_pdf(file_path):
    doc = fitz.open(file_path)
    text = ""

    for page in doc:
        text += page.get_text()

    questions = []

    pattern = r"(.*?)\nA\.\s*(.*?)\nB\.\s*(.*?)\nC\.\s*(.*?)\nD\.\s*(.*?)\nAnswer:\s*([A-D])"
    matches = re.findall(pattern, text, re.DOTALL)

    for match in matches:
        q, a, b, c, d, ans = match
        correct_index = ["A","B","C","D"].index(ans.strip())

        questions.append({
            "q": q.strip(),
            "o": [a.strip(), b.strip(), c.strip(), d.strip()],
            "a": correct_index
        })

    return questions
