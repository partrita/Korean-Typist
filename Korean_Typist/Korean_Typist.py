import reflex as rx
import time #type: ignore
import random

class State(rx.State):
    sentences = [
        "타이핑 연습을 시작하세요. 이 문장을 정확하게 입력해보세요.",
        "빠른 브라운 여우가 게으른 개를 뛰어넘었습니다.",
        "프로그래밍은 논리적 사고와 창의성이 필요한 분야입니다.",
        "시간은 금이라고 합니다. 하지만 경험은 다이아몬드입니다.",
        "끊임없는 노력과 열정이 성공의 열쇠입니다."
    ]
    text_to_type: str = sentences[0]
    user_input: str = ""
    cpm: float = 0
    cpm_display: str = "0.00"
    accuracy: float = 0
    start_time: float = 0
    

    def update_input(self, value: str):
        if self.start_time == 0:
            self.start_time = time.time()
        self.user_input = value
        self.calculate_cpm_and_accuracy()

    def calculate_cpm_and_accuracy(self):
        if self.start_time == 0:
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
        self.start_time = 0
        self.cpm = 0
        self.cpm_display = "0.00"
        self.accuracy = 0

def index():
    return rx.vstack(
        rx.heading("타이핑 연습 앱"),
        rx.text(State.text_to_type, color="blue"),
        rx.input(
            placeholder="여기에 타이핑하세요",
            on_change=State.update_input,
            value=State.user_input,
            width="300px"
        ),
        rx.hstack(
            rx.text(f"속도: {State.cpm_display} CPM", color="green"),
            rx.text(f"정확도: {State.accuracy:.1f}%", color="orange")
        ),
        rx.button("다음 문장", on_click=State.next_sentence)
    )

app = rx.App()
app.add_page(index)