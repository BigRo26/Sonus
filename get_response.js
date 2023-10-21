window.onload = function () {
    document
      .getElementById("chat-form")
      .addEventListener("submit", function (event) {
        // Prevent the form from submitting and refreshing the page
        event.preventDefault();

        let userInput = document.getElementById("user-input").value;
        let url = `/gpt4?user_input=${encodeURIComponent(userInput)}`;

        fetch(url)
          .then((response) => response.json())
          .then((data) => {
            let content = data.content;
            let resultDiv = document.getElementById("result");
            resultDiv.innerHTML = content;
          })
          .catch((error) => {
            console.error("Error fetching GPT-4 response:", error);
            let resultDiv = document.getElementById("result"); 
            if(userInput=="TEST"){resultDiv.innerHTML = "testd"};
          });
      });
  };