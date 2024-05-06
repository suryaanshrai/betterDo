console.log("index.js linked");


document.addEventListener("DOMContentLoaded", ()=>{
            document.querySelector("#newTaskButton").onclick=()=> {
                document.querySelector("#newReminderForm").style.display="none";
                document.querySelector("#newTaskForm").style.display="block";
            }
            document.querySelector("#newReminderButton").onclick= ()=>{
                document.querySelector("#newTaskForm").style.display="none";
                document.querySelector("#newReminderForm").style.display="block";
            }
            document.querySelectorAll(".finishTaskForm").forEach(button => {
                button.onclick=displayTaskForm;
            })
});

function displayTaskForm(id) {
    document.querySelector(`#task${id}`).style.display="block";
    document.querySelector(`#buttonid${id}`).style.display="none";
}

function rejectConfirmation(id) {
    document.querySelector(`#task${id}`).style.display="none";
    document.querySelector(`#buttonid${id}`).style.display="block";
}

function getGroup(group) {
    fetch("/taskgroup", {
        method:"POST",
        body: new FormData(document.querySelector(`#${group}form`)),
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        let taskstable=document.querySelector("#completedTasksTable");
        taskstable.innerHTML="";
        data['tasks'].forEach(task => {
            let rowdata=document.createElement('tr');
            let mytask=document.createElement('td');
            mytask.innerHTML=`${task.task}`
            let start=document.createElement('td');
            start.innerHTML=`${task.start_time}`;
            let end=document.createElement('td');
            end.innerHTML=`${task.end_time}`;
            let duration=document.createElement('td');
            duration.innerHTML=`${task.duration}`;
            let remark=document.createElement('td');;
            remark.innerHTML=`${task.remark}`;
            rowdata.append(mytask, start, end, duration,remark);
            taskstable.append(rowdata);
        });
        let exportdata=document.querySelector('#exportData');
        exportdata.value=group;
        let pagination=document.querySelector('#pagination');
        pagination.innerHTML="";
    });
    return false;
}