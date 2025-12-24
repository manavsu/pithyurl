<script lang="ts">
  import { SERVER_URL } from '$lib/config';

	let loading = $state(false);
	let long_url: string = $state('');
	let short_url_created = $state(false);
	let short_url = $state('');
	let error_message = $state('');
	let errored = $state(false);
	let copied = $state(false);

	async function handleURLSubmit(event: Event) {
		error_message = '';
		short_url = '';
		loading = true;
		event.preventDefault();
		try {
			let response = await shortenURL(long_url);
			short_url = response.url;
			short_url_created = true;
		} catch (error: any) {
			error_message = error.message;
			errored = true;
		}
		loading = false;
	}

async function shortenURL(url: string) {
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

	function copyToClipboard(text: string) {
		navigator.clipboard.writeText(text).then(() => {copied = true}).catch((err) => {
			console.error('Failed to copy: ', err);
		}).then(() => {
			setTimeout(() => {copied = false}, 400);
		});
	}
</script>

<div class="flex h-full w-full flex-col items-center justify-center gap-16">
	<div class="flex flex-col items-center gap-4">
		<h1 class="text-8xl text-primary">PithyURL</h1>
		<p class="text-4xl">Create Short URLs!</p>
	</div>
	<div class="h-50 flex pb-2">
		<div class="flex h-full flex-col items-center overflow-hidden py-2 transition-all duration-1000 ease-in-out {!short_url_created && !loading && !errored ? 'w-full' : 'w-0'}">
			<form onsubmit={handleURLSubmit} class="flex h-full flex-col items-center gap-8 px-8">
				<input id="longURL" type="url" class="w-96 input py-8 input-primary text-3xl" bind:value={long_url} required />
				<button type="submit" class="px-8 text-3xl btn btn-primary btn-wide">→</button>
			</form>
		</div>

		<div class="flex h-full flex-col items-center overflow-hidden py-2 transition-all duration-1000 ease-in-out {errored && !loading ? 'w-full' : 'w-0'}">
			<div class="flex flex-col items-center gap-4">
				<p class="text-nowrap text-error text-3xl">{error_message}</p>
				<button onclick={() => (errored = false)} class="btn btn-primary btn-wide px-8 text-3xl ">←</button>
			</div>
		</div>

		<div class="flex h-full flex-col items-center overflow-hidden py-2 transition-all duration-1000 ease-in-out {short_url_created && !loading ? 'w-full' : 'w-0'}">
			<div class="flex h-full flex-col items-center gap-4 px-8">
				<a href={short_url} target="_blank" class="text-nowrap text-3xl link link-primary">{short_url}</a>
				<button onclick={() => copyToClipboard(short_url)} class="btn btn-wide text-3xl transition  btn-outline {copied ? 'btn-success' : ''}">⧉</button>
				<button onclick={() => (short_url_created = false)} class="btn btn-success btn-wide text-3xl ">←</button>
			</div>
		</div>
		<div class="flex h-full flex-col items-center overflow-hidden duration-1000 transiton ease-in-out {loading ? 'w-full ' : 'w-0'}">
      <span class="loading loading-spinner loading-xl h-16 w-16"></span>
    </div>
	</div>
</div>
