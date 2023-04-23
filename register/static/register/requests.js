
document.addEventListener('DOMContentLoaded', function() {

    const openView = document.querySelector('#openRequests');
    const completedView = document.querySelector('#completedRequests');
    const assignedView = document.querySelector('#assignedRequests');
    const archivedView = document.querySelector('#archivedRequests');
    const newView = document.querySelector('#newRequests');
    
    
    
    

    const button = document.querySelectorAll('.btn-check');
    
    const completeBtn = document.querySelectorAll('button[name="complete"]');
    const holdBtn = document.querySelectorAll('button[name="hold"]');
    const confirmBtn = document.querySelectorAll('button[name="confirm"]');
    const cancelBtn = document.querySelectorAll('button[name="cancel"]');
    const resumeBtn = document.querySelectorAll('button[name="resume"]');
    
    completeBtn.forEach(function(completeBtn) {
        completeBtn.onclick = function() {
            console.log('Complete' + ' ' + completeBtn.value)
        }
    })

    holdBtn.forEach(function(holdBtn) {
        holdBtn.onclick = function() {
            console.log('Hold' + ' ' + holdBtn.value);
            document.querySelector(`div#note${holdBtn.value}`).style.display = 'block';
        }
    })

    confirmBtn.forEach(function(confirmBtn) {
        confirmBtn.onclick = function() {
            console.log('Confirm' + ' ' + confirmBtn.value)
        }
    })

    cancelBtn.forEach(function(cancelBtn) {
        cancelBtn.onclick = function() {
            console.log('Cancel' + ' ' + cancelBtn.value)
            document.querySelector(`div#note${cancelBtn.value}`).style.display = 'none';
        }
    })

    resumeBtn.forEach(function(resumeBtn) {
        resumeBtn.onclick = function() {
            console.log('Resume' + ' ' + resumeBtn.value)
        }
    })

    button.forEach(function(button) {
        button.onclick = function() {
            console.log(button.id);
            if (button.id == 'btnOpen') {
                console.log('Open');
                openView.style.display = 'block';
                completedView.style.display = 'none';
            }

            if (button.id == 'btnCompleted') {
                openView.style.display = 'none';
                completedView.style.display = 'block';
            }

            if (button.id == 'btnAssigned') {
                assignedView.style.display = 'block';
                archivedView.style.display = 'none';
                newView.style.display = 'none';
            }

            if (button.id == 'btnArchived') {
                assignedView.style.display = 'none';
                archivedView.style.display = 'block';
                newView.style.display = 'none';
            }

            if (button.id == 'btnNew') {
                assignedView.style.display = 'none';
                archivedView.style.display = 'none';
                newView.style.display = 'block';
            }

            
        }
    })
})