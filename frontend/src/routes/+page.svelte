<script lang="ts">
	import Loader from '$lib/loader.svelte';
	import { shortenURL } from './shorten';

	let loading = false;
	let long_url = '';
	let short_url = '';
	let error_message = '';

	async function handleURLSubmit(event: Event) {
		error_message = '';
		loading = true;
		event.preventDefault();
		try {
			let response = await shortenURL(long_url);
			short_url = response.url;
		} catch (error: any) {
			error_message = error.message;
		}
		loading = false;
	}
</script>

<div class="flex flex-col">
    <h1 class="text-6xl">PithyURL</h1>
    <p>Shorten your URL!</p>
    
    <div class="flex flex-col items-center overflow-hidden transition-all duration-1000 ease-in-out {!short_url && !loading ? 'w-[448px]' : 'w-0'}">
        <form onsubmit={handleURLSubmit} class="flex flex-row items-center gap-4">
            <label for="longURL" class="text-xl">URL:</label>
            <input id="longURL" type="url" class="rounded-full border-2 border-black bg-transparent px-5 py-1 text-xl focus:outline-none" bind:value={long_url} required />
            <button type="submit" class="rounded-xl text-xl transition hover:scale-110">→</button>
        </form>
    </div>
    <div class="flex flex-row items-center overflow-hidden transition-all duration-1000 ease-in-out gap-4 {short_url && !loading ? 'w-[340px]' : 'w-0'}">
        <a href={short_url} target="_blank" class="text-xl text-nowrap">{short_url}</a>
        <button onclick={() => short_url = ''} class="rounded-xl text-3xl transition hover:scale-110">←</button>
    </div>
    
    <div class="flex flex-col items-center overflow-hidden transition-all duration-1000 ease-in-out {error_message && !loading ? 'h-[439px]' : 'h-0'}">
        <p>{error_message}</p>
    </div>
    
    <div class="transition-all duration-1000 ease-in-out {loading ? 'h-40 w-40 p-10' : 'h-0 w-0'}"><Loader /></div>
</div>
