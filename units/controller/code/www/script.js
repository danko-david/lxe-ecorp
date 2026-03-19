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

async function streamTo(url, target) {
    try {
        const response = await fetch(url);
        const reader = response.body.getReader();
        const decoder = new TextDecoder();

        while (true) {
            const { value, done } = await reader.read();
            if (done)
				break;
			
			const chunk = decoder.decode(value, { stream: true });
            target.textContent += chunk;
            window.scrollTo(0, document.body.scrollHeight);
        }
    } catch (err) {
        console.error("Error occurred while streaming:", err);
    }
}

const runHooks = () =>{
		while (window.onReadyHooks.length > 0) window.onReadyHooks.shift()()
	};
	
if (document.readyState === 'interactive' || document.readyState === 'complete') {
	runHooks();
} else {
	document.addEventListener('readystatechange', () => {
		if (document.readyState === 'interactive') {
			runHooks();
		}
	});
};
console.log("JS loaded");