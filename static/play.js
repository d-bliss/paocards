const cards = JSON.parse('{{ cards|tojson|safe }}');
let currentCardIndex = {{ current_card_index }};
let currentCard = cards[currentCardIndex];
let isFlipped = {{ flip }};

// Select the element with id "card-name"
const cardName = document.querySelector("#card-name");
// Set the text of the element to the current card's rank and suit
cardName.innerText = `${currentCard.rank} of ${currentCard.suit}`;

// Select the element with id "card-attributes"
const cardAttributes = document.querySelector("#card-attributes");

// Select the element with id "flip-button"
const flipButton = document.querySelector("#flip-button");
// Add an event listener to the button that toggles the display of the card attributes
flipButton.addEventListener("click", () => {
    isFlipped = !isFlipped;
    cardAttributes.style.display = isFlipped ? "block" : "none";
});

// Select the element with id "next-button"
const nextButton = document.querySelector("#next-button");
// Add an event listener to the button that displays the next card in the cards array
nextButton.addEventListener("click", () => {
    currentCardIndex = (currentCardIndex + 1) % cards.length;
    currentCard = cards[currentCardIndex];
    cardName.innerText = `${currentCard.rank} of ${currentCard.suit}`;
    cardAttributes.innerHTML = `Person: ${currentCard.person}<br>
                                Action: ${currentCard.action}<br>
                                Object: ${currentCard.obj}`;
});

// javascript for the images

// Get a reference to the image and button elements
var image = document.getElementById("card-image");
var button = document.getElementById("next-button");

// create an array containing the file names of the images
var card_images = ["AC.png", "AD.png", "AH.png", "AS.png", "2C.png", "2D.png", "2H.png", "2S.png", "3C.png", "3D.png", "3H.png", "3S.png", "4C.png", "4D.png", "4H.png", "4S.png", "5C.png", "5D.png", "5H.png", "5S.png", "6C.png", "6D.png", "6H.png", "6S.png", "7C.png", "7D.png", "7H.png", "7S.png", "8C.png", "8D.png", "8H.png", "8S.png", "9C.png", "9D.png", "9H.png", "9S.png", "10C.png", "10D.png", "10H.png", "10S.png", "JC.png", "JD.png", "JH.png", "JS.png", "QC.png", "QD.png", "QH.png", "QS.png", "KC.png", "KD.png", "KH.png", "KS.png"];


// create a variable to keep track of the current image index
var currentIndex = 0;

// Add a click event listener to the button
button.addEventListener("click", function() {
  // increment the current index
  currentIndex++;
  if (currentIndex >= card_images.length) {
    currentIndex = 0;
  }
  // update the src attribute of the image
  image.src = "{{ url_for('static', filename='playing-cards/') }}" + card_images[currentIndex];
});
