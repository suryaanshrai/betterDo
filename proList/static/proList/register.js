console.log("register.js linked");


document.addEventListener("DOMContentLoaded", ()=>{
    document.querySelector("#usernameSuggestor").onclick=getRandomUsername;
});


function getRandomUsername(){
        let mybox=document.querySelector("#usernamebox");
        mybox.value="Just a sec...";
        mybox.disabled=true;

        fetch("https://api.api-ninjas.com/v1/randomuser", {
            headers: {
                'X-Api-Key':'aVTvW/d2pZr4A4k1GJuSAw==7Hqq0vAaiadgslB6'
            }
        }).
        then(response=>response.json()).
        then(data => {
            console.log(data.username);
            mybox.value=data.username;
            mybox.disabled=false;
            document.querySelector("#usernameSuggestor").innerHTML="Again";
        });
}