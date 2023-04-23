document.addEventListener('DOMContentLoaded', function() {

    const newView = document.querySelector('#newRequests');
    const newRequestsAmmount = document.querySelector('#newRequestsAmmount');
    const notesBtn = document.querySelectorAll('button[name="notesBtn"]');
    
   

    function update() {
        fetch('/update?q=newtasks')
        .then(response => response.text())
        .then(data => newView.innerHTML = data)
        .then(() => {
            var tasksCount = document.querySelector('#tasksCount').innerHTML;
            if (tasksCount > 0) {
                newRequestsAmmount.style.display = 'inline';
                newRequestsAmmount.innerHTML = tasksCount;
            }
            else
            {
                if (newRequestsAmmount) {
                    newRequestsAmmount.style.display = 'none';
                }
                
            }
        })
    } 
    
    // First update on DOM load and then every 1 minute
    update();
    setInterval(update, 60000);

    notesBtn.forEach(function(notesBtn) {
        notesBtn.onclick = function() {
            console.log(`Notes id=${notesBtn.value}`)
            fetch(`update?q=notes&id=${notesBtn.value}`)
            .then(response => response.text())
            .then(data => {
                const taskNote = document.querySelector(`#taskNotes${notesBtn.value}`);
                if (taskNote.style.display == 'none') {
                    taskNote.style.display = 'block'
                }  
               
                document.querySelector(`#taskNotes${notesBtn.value}`).innerHTML = data;
                const notesBtnHide = document.querySelectorAll('button[name="notesBtnHide"]');
                hideNotes(notesBtnHide)
            })
        }
    })

    function hideNotes(notesBtnHide) {
        notesBtnHide.forEach(function(notesBtnHide) {
            notesBtnHide.onclick = function() {
                console.log(`Hidden id=${notesBtnHide.value}`)
                document.querySelector(`#taskNotes${notesBtnHide.value}`).style.display = 'none';
            }
        })

    }
    
})