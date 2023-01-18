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

    const actionInput = document.querySelector(
        `input[name='action_${card.std_card_id}']`
    );
    actionInput.value = card.action;

    const objInput = document.querySelector(
        `input[name='obj_${card.std_card_id}']`
    );
    objInput.value = card.obj;
});

