'use strict';

// Once the document is fully loaded run this init function.
window.addEventListener('load', function init() {
    // Get the modal
    const modal = document.getElementById("myModal");
    const assignments = document.getElementsByClassName("edit");
    const modalClose = document.getElementsByClassName("close")[0];

    // When the user clicks on the button, open the modal
    for (let assignment of assignments) {
        assignment.onclick = function() {
            const { id, assignment, due_date, course } = this.dataset;

            modal.style.display = "block";
            const modalForm = document.getElementById("modal__form")
            const modalAssignment = document.getElementById("modal-assignment");
            const modalDue = document.getElementById("modal-due");
            const modalCourse = document.getElementById("modal-course");

            modalAssignment.value = assignment
            modalDue.value = due_date
            modalCourse.value = course

            modalForm.action = `/update/${id}`
        }
    }
    

    // When the user clicks on <span> (x), close the modal
    modalClose.onclick = function() {
    modal.style.display = "none";
    }

    // When the user clicks anywhere outside of the modal, close it
    window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
    }

    const checkboxes = document.getElementsByClassName('checkbox')
    for (let checkbox of checkboxes) {
        checkbox.addEventListener('change', function() {
            fetch( `/complete/${this.dataset.id}`, { method:'PUT'})
            .then(() => {
                location.reload()
                return false;
            })
            .catch((err) => alert(err))
        });
    }

    const deletes = document.getElementsByClassName('delete')
    for (let deleteButton of deletes) {
        deleteButton.addEventListener('click', function() {
            fetch( `/${this.dataset.id}`, { method:'DELETE'}).then(() => {
                location.reload()
                return false;
            }).catch((err) => alert(err))
        })
    }

    const dueDates = document.getElementsByClassName('table__due')
    for (let dueDate of dueDates) {
        const due = (new Date(dueDate.dataset.due_date)).toDateString().split(' ')

        dueDate.textContent = `${due[0]}, ${due.slice(1,due.length-1).join(' ')}`
    }

    document.getElementById('canvasButton').addEventListener('click', function(e) {
        e.preventDefault()
        e.target.disabled = true;
        e.target.className = " button loader";
        e.target.textContent = ""
        fetch('/canvas').then(() => {
            location.reload()
            return false;
        }).catch((err) => alert(err))
        
    })
})

