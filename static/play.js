const cards = JSON.parse('{{ cards|tojson|safe }}');
let currentCardIndex = {{ current_card_index }};
let currentCard = cards[currentCardIndex];
let isFlipped = {{ flip }};

const cardName = document.querySelector("#card-name");
cardName.innerText = `${currentCard.rank} of ${currentCard.suit}`;
const cardAttributes = document.querySelector("#card-attributes");
cardAttributes.innerHTML = `Person: ${currentCard.person}<br>
                            Action: ${currentCard.action}<br>
                            Object: ${currentCard.obj}`;

const flipButton = document.querySelector("#flip-button");
flipButton.addEventListener("click", () => {
    isFlipped = !isFlipped;
    cardAttributes.style.display = isFlipped ? "block" : "none";
});

const nextButton = document.querySelector("#next-button");
nextButton.addEventListener("click", () => {
    currentCardIndex = (currentCardIndex + 1) % cards.length;
    currentCard = cards[currentCardIndex];
    cardName.innerText = `${currentCard.rank} of ${currentCard.suit}`;
    cardAttributes.innerHTML = `Person: ${currentCard.person}<br>
                                Action: ${currentCard.action}<br>
                                Object: ${currentCard.obj}`;
});
