document.addEventListener('DOMContentLoaded', function() {

    const machineItem = document.querySelectorAll('button[name="machineItem"]');

    machineItem.forEach(function(machineItem) {
        machineItem.onclick = function() {
            console.log(`Machine id=${machineItem.value}`);
            const id = machineItem.value
            fetch(`/data?id=${id}`)
            .then(response => response.json())
            .then(data => {
                document.querySelector(`span[name="newCount${id}"]`).innerHTML = data.new;
                document.querySelector(`span[name="ongoingCount${id}"]`).innerHTML = data.ongoing;
                document.querySelector(`span[name="completedCount${id}"]`).innerHTML = data.completed;
            })
        }
    })
})