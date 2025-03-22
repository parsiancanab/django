
function updateDateTime() {
    const now = new Date();
    const dateOptions = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
    const timeOptions = { hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: true };

    const formattedDate = now.toLocaleDateString(undefined, dateOptions);
    const formattedTime = now.toLocaleTimeString(undefined, timeOptions);

    const datetimeElement = document.getElementById('demo');
    datetimeElement.textContent = `Today is ${formattedDate}, and the current time is ${formattedTime}.`;
}

// Initial call to update the date and time
updateDateTime();

// Set up an interval to update the date and time every second (optional)
setInterval(updateDateTime, 1000);

const currencyContainer = document.getElementById('currency-container');

      fetch('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd')
          .then(response => response.json())
          .then(data => {
              const bitcoinPrice = data.bitcoin.usd;
              const ethereumPrice = data.ethereum.usd;

              console.log('Bitcoin Price in USD:', bitcoinPrice);
              console.log('Ethereum Price in USD:', ethereumPrice);

              currencyContainer.innerHTML = `
                  <p>Bitcoin (BTC): $${bitcoinPrice}</p>
                  <p>Ethereum (ETH): $${ethereumPrice}</p>
              `;
          })