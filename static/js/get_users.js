document.addEventListener('DOMContentLoaded', async () => {
    try {
        const response = await fetch('/users', {
        method: 'GET',
        headers: {
            'api-key':'9LrazloGBYZTniI3qkzWKkGTXvdqPkXB'
        }
    });
        const data = await response.json();
        const outUl = document.getElementById("users-content")
       for (let obj of data){
            const Liel = document.createElement("li")
            Liel.textContent = `${obj.user_id} ${obj.username} ${obj.fullname} ${obj.role} ${obj.ref}`;
            outUl.appendChild(Liel);
       }

    } catch(error){
        console.log(error)
    }
});