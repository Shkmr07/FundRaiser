const url = 'http://127.0.0.1:8000/fundraiser/'

const getElement = (data) =>{

    const list = document.getElementById('sliding-bar')
    list.innerHTML = '';
    
    data.forEach((el)=>{
        
        const div = document.createElement('div')
        const h = document.createElement('h3')
        const image = document.createElement('img')
        const a = document.createElement('a')
        a.textContent = 'Donate'
        a.href ='./donation.html'
        image.src = el.image
        div.className = 'listDiv'
        h.textContent = el.title

        a.addEventListener('click',()=>{

            localStorage.setItem('userId', el.id)
        })
        
        div.append(image,h,a)
        list.appendChild(div)
        
    })
}


const getLogout = ()=>{
    const sign = document.getElementById('signin')
    const token = localStorage.getItem('token')
    const logout = document.getElementById('logout')
    if (token){
        sign.style.display = 'none'
        logout.style.display = 'block'

    }
    else{
        logout.style.display = 'none'
        sign.style.display = 'block'
    }
}

getLogout()



const fetchDetail = async () =>{

    try{

        const res = await fetch(`${url}campaignlist/`)
        const data = await res.json()
        getElement(data)
        console.log(data)

    } catch  (error){
        console.log('Something Wrong in FetchDetail',error)
    }
}

fetchDetail()


document.getElementById('logout').addEventListener('click', async () => {
    try {
        const res = await fetch(`${url}logout/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            credentials: 'include' // Ensure cookies are sent with the request
        });

        if (!res.ok) {
            throw new Error('Logout failed');
        }

        const data = await res.json();
        console.log('Logout Successful:', data);

        // Remove the token from local storage
        localStorage.removeItem('token');

        // Clear cookies if needed
        document.cookie = 'jwtToken=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/;';
        document.cookie = 'csrftoken=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/;';

        // Optionally redirect or reload
        alert('Logout Successful');
        // window.location.href = './index.html'; // Redirect to the login page

    } catch (error) {
        console.error('Error during logout:', error);
        alert(`Error: ${error.message}`);
    }
});