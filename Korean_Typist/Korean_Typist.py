import reflex as rx
import time #type: ignore
import random
import json

with open("sentences.json", 'r', encoding='utf-8') as file:
    text = json.load(file)['sentences']

class State(rx.State):
    sentences = text
    text_to_type: str = sentences[0]
    user_input: str = ""
    cpm: float = 0.0
    cpm_display: str = "0.00"
    accuracy: float = 0.0
    start_time: float = 0.0
    

    def update_input(self, value: str):
        if self.start_time == 0.0:
            self.start_time = time.time()
        self.user_input = value
        self.calculate_cpm_and_accuracy()

    def calculate_cpm_and_accuracy(self):
        if self.start_time == 0.0:
            return
        
        elapsed_time = time.time() - self.start_time
        correct_chars = sum(1 for a, b in zip(self.text_to_type, self.user_input) if a == b)
        total_chars = max(len(self.user_input), 1)
        
        if elapsed_time > 0:
            self.cpm = (correct_chars / elapsed_time) * 60
            self.cpm_display = f"{self.cpm:.2f}"
        else:
            self.cpm = 0
            self.cpm_display = "0.00"
        
        self.accuracy = (correct_chars / total_chars) * 100

    def next_sentence(self):
        self.text_to_type = random.choice(self.sentences)
        self.user_input = ""
        self.start_time = 0.0
        self.cpm = 0.0
        self.cpm_display = "0.00"
        self.accuracy = 0.0

def index():
    return rx.vstack(
        rx.heading("타이핑 연습 앱", align="center"),  # 제목을 가운데 정렬
        rx.hstack(
            rx.text(f"속도: {State.cpm_display} CPM", color="green", size="lg"),  # 속도 텍스트 크기 조정
            rx.text(f"정확도: {State.accuracy:.1f}%", color="orange", size="lg"),  # 정확도 텍스트 크기 조정
            spacing="5",
            align="center"  # 속도와 정확도 텍스트를 가운데 정렬
        ),
        rx.text(State.text_to_type, color="blue", align="center"),  # 문장도 가운데 정렬
        rx.input(
            placeholder="여기에 타이핑하세요",
            on_change=State.update_input,
            value=State.user_input,
            width="400px",  # 입력 필드의 너비를 늘림
            height="40px",  # 입력 필드의 높이를 늘림
            size="lg",
            align="center"  # 입력 필드도 가운데 정렬
        ),
        rx.button("다음 문장", on_click=State.next_sentence, width="200px", align="center"),  # 버튼을 가운데 정렬
        align="center" 
    )

app = rx.App()
app.add_page(index)