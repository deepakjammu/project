const handleForm = (e) => {
    
    const username = document.getElementById('username').value
    localStorage.setItem('username', username)
    
}