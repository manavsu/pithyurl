<script lang="ts">
	import Loader from '$lib/loader.svelte';
	import { shortenURL } from './shorten';

	let loading = false;
	let long_url = '';
	let short_url_created = false;
	let short_url = '';
	let error_message = '';
	let errored = false;
	let copied = false;

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

	function copyToClipboard(text: string) {
		navigator.clipboard.writeText(text).then(() => {copied = true}).catch((err) => {
			console.error('Failed to copy: ', err);
		}).then(() => {
			setTimeout(() => {copied = false}, 400);
		});
	}
</script>

<div class="flex h-full w-full flex-col items-center justify-center gap-20">
	<div class="flex flex-col items-center gap-4">
		<h1 class="text-8xl">PithyURL</h1>
		<p class="text-4xl">Create Short URLs!</p>
	</div>

	<div class="h-50 flex flex-row pb-2">
		<div class="flex h-full flex-col items-center overflow-hidden py-2 transition-all duration-1000 ease-in-out {!short_url_created && !loading && !errored ? 'w-full' : 'w-0'}">
			<form onsubmit={handleURLSubmit} class="flex h-full flex-col items-center gap-4 px-8">
				<input id="longURL" type="url" class="w-96 rounded-full border-2 border-white bg-transparent px-5 py-1 text-3xl focus:outline-none" bind:value={long_url} required />
				<button type="submit" class="rounded-full border-2 border-white bg-white px-8 text-3xl text-black transition hover:scale-110">→</button>
			</form>
		</div>

		<div class="flex h-full flex-col items-center overflow-hidden py-2 transition-all duration-1000 ease-in-out {errored && !loading ? 'w-full' : 'w-0'}">
			<div class="flex flex-col items-center gap-4">
				<p class="text-nowrap text-3xl">{error_message}</p>
				<button onclick={() => (errored = false)} class="rounded-full border-2 border-white px-8 text-3xl transition hover:scale-110">←</button>
			</div>
		</div>

		<div class="flex h-full flex-col items-center overflow-hidden py-2 transition-all duration-1000 ease-in-out {short_url_created && !loading ? 'w-full' : 'w-0'}">
			<div class="flex h-full flex-col items-center gap-4 px-8">
				<a href={short_url} target="_blank" class="text-nowrap rounded-full bg-white px-5 py-1 text-3xl text-black transition hover:scale-110">{short_url}</a>
				<button onclick={() => copyToClipboard(short_url)} class="rounded-full border-2  px-16 text-3xl transition hover:scale-110 {copied ? 'text-green-600 border-green-600' : 'text-white border-white'}">⧉</button>
				<button onclick={() => (short_url_created = false)} class="rounded-full border-2 border-white px-8 text-3xl transition hover:scale-110">←</button>
			</div>
		</div>
		<!-- <div class="transition-all duration-1000 ease-in-out {loading ? 'w-full' : 'w-0'}"><Loader /></div> -->
	</div>
</div>
