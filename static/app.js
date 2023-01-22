/*
const cards = cardsData;
// This code is used to populate the form inputs with data passed in the "cardsData" variable.
// It uses the .forEach method to iterate through each card in the "cards" array and sets the value
// of the input fields with the corresponding data from the card object (card.person, card.action, card.obj)
// The input fields are selected by their name attribute, which includes the std_card_id of the card.
cards.forEach((card) => {
    const personInput = document.querySelector(
        `input[name='person_${card.std_card_id}']`
    );
    personInput.value = card.person;
    personInput.classList.add("bold-text");


    const actionInput = document.querySelector(
        `input[name='action_${card.std_card_id}']`
    );
    actionInput.value = card.action;
    actionInput.classList.add("bold-text");


    const objInput = document.querySelector(
        `input[name='obj_${card.std_card_id}']`
    );
    objInput.value = card.obj;
    objInput.classList.add("bold-text");
});

<script>
    // parse the cards data passed from the backend
    const cards = JSON.parse('{{ cards|tojson|safe }}');
</script>
*/