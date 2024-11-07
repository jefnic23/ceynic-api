<script lang="ts">
	import { createEventDispatcher } from 'svelte';

	const dispatch = createEventDispatcher();
	let files: File[] = [];

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

	let fileInput: HTMLInputElement;
</script>

<div
	class="dropzone"
	on:dragover|preventDefault
	on:drop={handleDrop}
	on:click={() => fileInput.click()}
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
			<div class="image-wrapper">
				<img src={URL.createObjectURL(file)} alt="Preview" class="image" />
				<button class="remove-btn" on:click={(e) => removeImage(index, e)}>✕</button>
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
		width: 100px;
		height: 100px;
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
	}
</style>
