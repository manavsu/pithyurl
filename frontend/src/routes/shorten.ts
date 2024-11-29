import { SERVER_URL } from '$lib/config';

export async function shortenURL(url: string) {
	const response = await fetch(`${SERVER_URL}/urls`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify({ url })
	});
	if (!response.ok) {
		throw new Error(response.status + response.statusText);
	}
	return response.json();
}
