const url = "static/2015-Building-Code.pdf";

async function renderPage(doc, pageNumber) {
  if (pageNumber >= 1 && pageNumber <= doc._pdfInfo.numPages) {
    // Fetch the page
    const page = await doc.getPage(pageNumber);

    // Set the viewport
    const viewport = page.getViewport({ scale: 1.5 });

    // Set the canvas dimensions to the PDF page dimensions
    const canvas = document.getElementById("canvas");
    const context = canvas.getContext("2d");
    canvas.height = viewport.height;
    canvas.width = viewport.width;

    // Render the PDF page into the canvas context
    await page.render({
      canvasContext: context,
      viewport: viewport,
    }).promise;

    // Create and position the text layer div
    const textLayerDiv = document.getElementById("text-layer");
    textLayerDiv.style.width = `${viewport.width}px`;
    textLayerDiv.style.height = `${viewport.height}px`;

    // Render the text layer
    const textContent = await page.getTextContent();
    const textLayer = new TextLayerBuilder({
      textLayerDiv,
      pageIndex: pageNumber - 1,
      viewport,
    });
    textLayer.setTextContent(textContent);
    textLayer.render();
  } else {
    console.log("Please specify a valid page number");
  }
}

async function sendMessage() {
  const chatInputField = document.getElementById("inputFieldValue");
  const chatMessages = document.querySelector(".chat-messages");
  const message = chatInputField.value;

  const selectedTextElement = document.querySelector(".selected-text");
  const selectedText = selectedTextElement
    ? selectedTextElement.textContent
    : "";

  if (message.trim() !== "" || selectedText.trim() !== "") {
    const messageContainer = document.createElement("div");
    messageContainer.classList.add("chatMessageContainer");

    const messageElement = document.createElement("div");
    messageElement.classList.add("chatMessage", "user-message");

    messageElement.textContent =
      message + (selectedText ? " [Selected text: " + selectedText + "]" : "");

    chatMessages.appendChild(messageContainer);

    const messageContainers = document.querySelectorAll(
      ".chatMessageContainer"
    );
    const lastMessageContainer =
      messageContainers[messageContainers.length - 1];
    lastMessageContainer.appendChild(messageElement);

    const loadingElement = document.createElement("div");
    loadingElement.setAttribute("id", "loadingMessage");
    loadingElement.setAttribute("style", "display: none;");
    loadingElement.setAttribute("class", "simpleText");
    loadingElement.textContent = "Thinking";

    const innerLoadingelement = document.createElement("span");
    innerLoadingelement.setAttribute("id", "dots");

    loadingElement.appendChild(innerLoadingelement);

    lastMessageContainer.appendChild(loadingElement);

    var loadingInterval = startLoadingAnimation();

    chatInputField.value = "";
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }

  if (message.trim() !== "" || selectedText.trim() !== "") {
    // Send message and selected text to server
    const response = await fetch("/process_message", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message, selectedText }),
    });

    // Check if the request was successful
    if (response.ok) {
      const responseData = await response.json();
      const data = responseData.responseText;
      const relatedChunks = responseData.relatedChunks;

      console.log(
        "yooooooooooooooooooooooooooooooooooooooooooooooooo!!!!!!!!!!!!!!!"
      );
      console.log(data);

      relatedSections = [];

      for (var i = 0; i < relatedChunks.length; i++) {
        var chunk = relatedChunks[i];
        var divClass = chunk.class;
        var divId = chunk.id;

        sectionDiv = document.createElement("a");
        sectionDiv.setAttribute("href", "content.html#" + divId);
        sectionDiv.setAttribute("class", "relatedSection");

        if (divClass) {
          sectionDiv.textContent = divClass;
        } else {
          sectionDiv.textContent = "Related Section";
        }

        relatedSections.push(sectionDiv); // Use push to add the element to the array
      }

      // Crete AI response text bubble
      const messageContainer = document.createElement("div");
      messageContainer.classList.add("chatMessageContainer");

      const messageElement = document.createElement("div");
      messageElement.classList.add("chatMessage", "airesponse");

      // Replace line and paragraph breaks with <br> tags

      messageElement.innerHTML = data.replace(/(?:\r\n|\r|\n)/g, "<br>");

      let messageContainers;
      messageContainers = document.querySelectorAll(".chatMessageContainer");

      let lastMessageContainer;

      stopLoadingAnimation(loadingInterval);
      lastMessageContainer = messageContainers[messageContainers.length - 1];
      lastMessageContainer.appendChild(messageElement);

      // Create AI response section bubbles
      const sectionsContainer = document.createElement("div");
      sectionsContainer.classList.add("chatMessageContainer");

      const sectionsElement = document.createElement("div");
      sectionsElement.classList.add("airesponse", "sections");
      sectionsElement.textContent = "Sources:";
      for (var i = 0; i < relatedSections.length; i++) {
        section = relatedSections[i];
        sectionsElement.appendChild(section);
        console.log(section);
      }

      chatMessages.appendChild(sectionsContainer);

      messageContainers = document.querySelectorAll(".chatMessageContainer");

      lastMessageContainer = messageContainers[messageContainers.length - 1];
      lastMessageContainer.appendChild(sectionsElement);

      var baseUrl = "{{ url_for('iframe', filename='') }}";

      if (sectionsElement) {
        const linksToUpdateIframe = sectionsElement.querySelectorAll("a");
        console.log("here!!!!!!!!!!!!!!!!!!!!!!!!");

        console.log(linksToUpdateIframe);
        for (var i = 0; i < linksToUpdateIframe.length; i++) {
          section = linksToUpdateIframe[i];
          console.log(i);
          console.log(section.getAttribute("href")); // Use getAttribute to access href
        }
        console.log("here!!!!!!!!!!!!!!!!!!!!!!!!");

        linksToUpdateIframe.forEach(function (linkToUpdateIframe) {
          linkToUpdateIframe.addEventListener("click", function (event) {
            event.preventDefault(); // Prevent the default link behavior

            const codeContentiFrame =
              document.querySelector(".codeContentiFrame");

            if (codeContentiFrame) {
              // Use the entire href attribute value
              const href = linkToUpdateIframe.getAttribute("href");
              codeContentiFrame.src = baseUrl + href;
            }
          });
        });
      }
    } else {
      console.error("Error sending message to the server");
    }
    var div = document.querySelector(".chat-messages");
    div.scrollTop = div.scrollHeight;
  }
}

// document.querySelector("embed").addEventListener("mouseup", function () {
//   const selectedText = window.getSelection();
//   console.log("oii mayte");
//   console.log(selectedText);

//   // Clear previous selections
//   const previousSelections = document.querySelectorAll(".selected-text");
//   previousSelections.forEach((selection) => {
//     const parent = selection.parentNode;
//     while (selection.firstChild) {
//       parent.insertBefore(selection.firstChild, selection);
//     }
//     parent.removeChild(selection);
//   });

//   if (selectedText.toString().trim() !== "") {
//     const range = selectedText.getRangeAt(0);
//     const span = document.createElement("span");
//     span.className = "selected-text";
//     range.surroundContents(span);
//   }
// });

// Update codeContent iFrame to sidebar selected item
var baseUrl = "{{ url_for('iframe', filename='') }}";

document.addEventListener("DOMContentLoaded", function () {
  const sideBariFrame = document.querySelector(".sideBariFrame");
  if (sideBariFrame) {
    sideBariFrame.addEventListener("load", function () {
      const linksToUpdateIframe =
        sideBariFrame.contentDocument.querySelectorAll(".bookmark");
      linksToUpdateIframe.forEach(function (linkToUpdateIframe) {
        linkToUpdateIframe.addEventListener("click", function (event) {
          event.preventDefault(); // Prevent the default link behavior
          const codeContentiFrame =
            document.querySelector(".codeContentiFrame");
          if (codeContentiFrame) {
            // Use the entire href attribute value
            const href = linkToUpdateIframe.getAttribute("href");
            codeContentiFrame.src = baseUrl + href;
          }
        });
      });
    });
  }
});

document.addEventListener("DOMContentLoaded", function () {
  var isHidden = false;
  var btn = document.querySelector(".toggle-btn");
  var div = document.querySelector(".sidebar");
  btn.addEventListener("click", function () {
    if (isHidden) {
      div.classList.remove("hidden");
      btn.textContent = "<";
    } else {
      div.classList.add("hidden");
      btn.textContent = ">";
    }
    isHidden = !isHidden;
  });
});

document
  .getElementById("inputFieldValue")
  .addEventListener("keypress", function (event) {
    if (event.keyCode === 13) {
      // 13 is the key code for Enter
      event.preventDefault(); // Prevent the default action to stop submitting the form directly
      sendMessage();
    }
  });

function startLoadingAnimation() {
  var loadingMessage = document.getElementById("loadingMessage");
  var dots = document.getElementById("dots");
  var numDots = 0;
  loadingMessage.style.display = "inline";

  var interval = setInterval(function () {
    dots.textContent += ".";
    numDots++;

    if (numDots === 4) {
      dots.textContent = "";
      numDots = 0;
    }
  }, 500); // Adjust the interval time as needed

  return interval;
}

function stopLoadingAnimation(interval) {
  clearInterval(interval);
  var loadingMessage = document.getElementById("loadingMessage");
  if (loadingMessage) {
    loadingMessage.remove(); // Remove the element from the DOM
  }
}
