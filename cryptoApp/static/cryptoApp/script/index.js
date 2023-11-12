
// const coinDetailModal = document.getElementById('coinDetailModal')
// console.log(coinDetailModal)
// if (coinDetailModal) {
//   coinDetailModal.addEventListener('show.bs.modal', event => {
//     const button = event.relatedTarget
//     const recipient = button.getAttribute('data-bs-whatever')
//     console.log("recipient", recipient.name)
//     const modalTitle = coinDetailModal.querySelector('.modal-title')
//     const modalBodyInput = coinDetailModal.querySelector('.modal-body input')
//
//     modalTitle.textContent = `New message to ${recipient}`
//     modalBodyInput.value = recipient
//   })
// }

function redirection(id) {
    window.location.href = `coin/${id}`
}

