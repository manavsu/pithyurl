<script lang="ts">
	import '$lib/app.css';

	let { children } = $props();
</script>


<style lang="postcss">
	@import url('https://fonts.googleapis.com/css2?family=Patrick+Hand&display=swap');

	:global(html) {
	  @apply bg-black text-white;
	  caret-color: white;
	}
	
	* {
		/* @apply scrollbar-thin scrollbar-thumb-gray-500 scrollbar-track-transparent; */
		font-family: 'Patrick Hand', cursive;
	}
</style>

<div class="h-dvh flex flex-col overscroll-contain overflow-auto">
	{@render children()}
</div>
