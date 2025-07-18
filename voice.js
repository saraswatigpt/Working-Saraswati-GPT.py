function startListening() {
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = 'en-US';
    recognition.onresult = function(event) {
        const transcript = event.results[0][0].transcript;
        document.getElementById('question').value = transcript;
    };
    recognition.start();
}