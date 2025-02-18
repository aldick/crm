function copyText() {
	const target = document.querySelector("#copy");
	const text = target.textContent
		.replace(/^\s+/gm, "")
		.trim();

	navigator.clipboard.writeText(text).then(() => {
		alert("Copied!")
	});

	console.log(text);
}