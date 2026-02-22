function ajax(url, result)
{
	fetch(url)
	.then((response) => {
		if (!response.ok) {
			throw Error(response.statusText);
		}
		return response;
	})
	.then((response) => response.text())
	.then(result)
}

function ajaxResultSetTo(url, targetId)
{
	return function()
	{
		ajax(url, (r)=>
		{
			document.getElementById(targetId).innerHTML = r.trim();
		});
	}
}

function loopRun(ms, func)
{
	func()
	setTimeout(()=>{loopRun(ms, func)}, ms);
}

document.addEventListener('click', function(e) {
	console.log(e);
    if (e.target && e.target.classList.contains('popup-activate')) {
		
        const container = e.target.parentElement;
        const dataDiv = container.querySelector('.popup-data');
        
        if (dataDiv) {
            const overlay = document.getElementById('popupOverlay');
            const content = document.getElementById('popupContent');
            
            content.innerHTML = dataDiv.innerHTML;
            overlay.style.display = 'flex';
        }
    }
});

function closePopup() {
    document.getElementById('popupOverlay').style.display = 'none';
}

console.log("JS loaded")