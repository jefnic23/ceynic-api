<script lang="ts">
	import { onMount } from 'svelte';
	import { createEventDispatcher } from 'svelte';

	export let previews: string[];
	export let thumbnail: string | null;

	const dispatch = createEventDispatcher();
	let files: File[] = [];

	$: if (!thumbnail && files.length > 0) {
		thumbnail = files[0].name;
	}

	// Triggered when images are dropped into the dropzone
	function handleDrop(event: DragEvent) {
		event.preventDefault();
		if (event.dataTransfer) {
			const newFiles = Array.from(event.dataTransfer.files).filter((file) =>
				file.type.startsWith('image/')
			);
			files = [...files, ...newFiles];
			dispatch('change', { files });
		}
	}

	// Triggered when images are selected through file input
	function handleSelect(event: Event) {
		const target = event.target as HTMLInputElement;
		const selectedFiles = target.files ? Array.from(target.files) : [];
		const newFiles = selectedFiles.filter((file) => file.type.startsWith('image/'));
		files = [...files, ...newFiles];
		dispatch('change', { files });
	}

	// Removes a selected image from the list
	function removeImage(index: number, event: MouseEvent) {
		event.stopPropagation(); // Prevents triggering the dropzone click event
		files = files.filter((_, i) => i !== index);
		dispatch('change', { files });
	}

	function selectThumbnail(filename: string, event: MouseEvent | KeyboardEvent) {
		event.stopPropagation(); // Prevents triggering the dropzone click event
		thumbnail = filename;
		dispatch('thumbnailChange', { thumbnail });
	}

	async function createFileFromImage(imageUrl: string) {
		const filename = imageUrl.split('/').at(-1);
		const response = await fetch(imageUrl);
		const blob = await response.blob();
		const file = new File([blob], filename as string, { type: blob.type });
		return file;
	}

	let fileInput: HTMLInputElement;

	onMount(async () => {
		if (previews.length > 0) {
			Promise.all(previews.map(createFileFromImage))
				.then((resolvedFiles) => {
					files = resolvedFiles;
				})
				.catch((error) => console.error('Error loading files:', error));
		}
	});
</script>

<div
	class="dropzone"
	role="button"
	aria-label="Image upload dropzone. Click or press Enter to upload images."
	tabindex="0"
	on:dragover|preventDefault
	on:drop={handleDrop}
	on:click={() => fileInput.click()}
	on:keydown={(e) => e.key === 'Enter' && fileInput.click()}
>
	<p>Drag & drop images here, or click to select</p>
	<input
		type="file"
		accept="image/*"
		multiple
		bind:this={fileInput}
		on:change={handleSelect}
		style="display: none;"
	/>
	<div class="image-preview">
		{#each files as file, index}
			<div
				class="image-wrapper {thumbnail === file.name ? 'thumbnail' : ''}"
				role="button"
				aria-label="Click an image to make it the product thumbnail."
				aria-pressed={thumbnail === file.name}
				tabindex="0"
				on:click={(e) => selectThumbnail(file.name, e)}
				on:keydown={(e) => e.key === 'Enter' && selectThumbnail(file.name, e)}
			>
				<img src={URL.createObjectURL(file)} alt="Preview" class="image" />
				{#if thumbnail === file.name}
					<span class="thumbnail-indicator">Thumbnail</span>
				{/if}
				<button class="remove-btn" aria-label="Remove image" on:click={(e) => removeImage(index, e)}
					>&times;</button
				>
			</div>
		{/each}
	</div>
</div>

<style>
	.dropzone {
		border: 2px dashed #ccc;
		padding: 20px;
		display: flex;
		flex-direction: column;
		align-items: center;
		cursor: pointer;
		transition: background-color 0.2s;
	}

	.dropzone:hover {
		background-color: #f0f0f0;
	}

	.image-preview {
		display: flex;
		flex-wrap: wrap;
		margin-top: 10px;
	}

	.image-wrapper {
		position: relative;
		margin: 5px;
	}

	.image {
		width: 144px;
		height: 144px;
		object-fit: cover;
		border-radius: 5px;
	}

	.remove-btn {
		position: absolute;
		top: 5px;
		right: 5px;
		background: rgba(255, 255, 255, 0.7);
		border: none;
		border-radius: 50%;
		cursor: pointer;
		transition:
			transform 0.2s ease,
			background-color 0.2s ease;
	}

	.remove-btn:hover {
		transform: scale(1.2);
		background-color: rgba(255, 0, 0, 0.8);
		color: white;
	}

	.thumbnail-indicator {
		position: absolute;
		bottom: 0;
		left: 0;
		background: rgba(0, 128, 0, 0.6);
		color: white;
		padding: 2px 5px;
		font-size: 0.8em;
		border-radius: 0 0 0 3px;
	}

	.image-wrapper.thumbnail {
		border: 2px solid green;
		border-radius: 5px;
	}
</style>
