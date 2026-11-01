
const input = document.getElementById("user-input");
const chatBox = document.getElementById("chat-box");
const sendButton = document.getElementById("send-button");


// 메시지를 화면에 추가하는 함수
function addMessage(message, type) {

    const messageDiv = document.createElement("div");
    messageDiv.className = "message " + type;

    const bubble = document.createElement("div");
    bubble.className = "bubble";

    // 사용자 입력을 HTML로 해석하지 않고 일반 문자로 표시
    bubble.textContent = message;

    messageDiv.appendChild(bubble);
    chatBox.appendChild(messageDiv);

    // 항상 최신 메시지로 이동
    chatBox.scrollTop = chatBox.scrollHeight;
}


// 질문 전송 함수
async function sendMessage() {

    const message = input.value.trim();

    if (message === "") {
        return;
    }

    // 사용자 질문 표시
    addMessage(message, "user");

    input.value = "";
    sendButton.disabled = true;

    try {

        // Flask 서버에 질문 전달
        const response = await fetch("/chat", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                message: message
            })

        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error("답변을 가져오지 못했습니다.");
        }

        // 선택된 답변 표시
        addMessage(data.answer, "bot");

    } catch (error) {

        addMessage(
            "서버와 연결할 수 없습니다. 다시 시도해주세요.",
            "bot"
        );

        console.error(error);

    } finally {

        sendButton.disabled = false;
        input.focus();

    }
}


// Enter 키로 메시지 전송
input.addEventListener("keydown", function(event) {

    if (event.key === "Enter") {
        sendMessage();
    }

});
