const url = 'http://127.0.0.1:8000/fundraiser/'

campaign_id = localStorage.getItem('userId')



const getDonor = (data) => {
    const list = document.getElementById('donorlist');
    list.innerHTML = ''; // Clear any existing content

    // Filter the data by the specified campaign ID
    let filterValue = data.filter(el => el.campaign === Number(campaign_id));

    // Iterate over the filtered results and create list items
    filterValue.forEach(donor => {
        const listItem = document.createElement('li');
        listItem.textContent = `${donor.donor_detail.firstname} paid ${donor.amount}`;
        let user = localStorage.getItem('token')
        let name = localStorage.getItem('username')
        if (user){

            if(donor.donor.username != name){

                const donation = document.createElement('button')
                donation.addEventListener('click', async ()=>{
                
                    try{
                        const amount = prompt("Enter the amount you want to donate:");
                        const res = await fetch(`${url}donation/`,{method : 'POST', headers : {'Content-Type' : 'application/json'},body : JSON.stringify({'campaign': campaign_id, 'amount' : Number(amount)})})
                        if (res.ok){
                            alert('Thank you for donation')
                        }
                        else alert('Failed to proccess donation')

                    } catch (error){
                        console.error('Something Went Wrong Donation Button',error)
                    }

                    listItem.appendChild(donation)
                })

            }
        }
        
        list.appendChild(listItem);
    });

    

    // If no donors are found for the campaign, display a message
    if (filterValue.length === 0) {
        const noDataItem = document.createElement('li');
        noDataItem.textContent = 'No donors found for this campaign.';
        list.appendChild(noDataItem);
    }
};



const fetchDonor = async () =>{

    try{
        
        const res = await fetch(`${url}donationlist/`)
        const data = await res.json()
        getDonor(data)


    } catch (error) {
        console.error('Something Went Wrong in fetchDonor')
    }

}

fetchDonor()


const getElement = (data) => {

    // Get the container where you want to display the campaign details
    const cont = document.getElementById('cont');
    cont.innerHTML = ''; // Clear any existing content

    // Create elements to display the campaign details
    const title = document.createElement('h2');
    const image = document.createElement('img');
    const description = document.createElement('p');
    const goalAmount = document.createElement('p');
    const currentAmount = document.createElement('p');
    const createdAt = document.createElement('p');

    // Set the content of the elements
    title.textContent = data.title;
    image.src = `http://127.0.0.1:8000${data.image}`;
    description.textContent = data.description;
    goalAmount.textContent = `Goal Amount: ₹${parseFloat(data.goal_amount).toLocaleString()}`;
    currentAmount.textContent = `Current Amount: ₹${parseFloat(data.current_amount).toLocaleString()}`;
    createdAt.textContent = `Created At: ${new Date(data.created_at).toLocaleString()}`;

    // Set image attributes
    image.alt = data.title;
    image.style.width = '100%'; // Adjust width as needed
    image.style.maxWidth = '600px'; // Ensure the image doesn't get too large

    // Append the elements to the container
    cont.appendChild(title);
    cont.appendChild(image);
    cont.appendChild(description);
    cont.appendChild(goalAmount);
    cont.appendChild(currentAmount);
    cont.appendChild(createdAt);
};



const fetchCampaign = async ()=>{

    try{

        const res = await fetch(`${url}getcampaign/${campaign_id}`)
        const data = await res.json()
        getElement(data)

    } catch (error) {
        console.error('Something Went Wrong in Donation.js')
    }
}

fetchCampaign()