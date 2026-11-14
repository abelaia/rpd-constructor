import {ref} from 'vue';
import {generateWord} from '@/core/api/documents';
import {getErrorMessage} from '@/core/helpers/getErrorMessage';
import {saveFile} from '@/core/helpers/saveFile';
import {useToastStore} from '@/core/stores/toast';
import {toGenerateRequest} from '@/core/utils/programs';

const DOWNLOADED_MESSAGE = 'Документ скачан';

export function useDownloadProgram() {
    const toastStore = useToastStore();

    const isDownloading = ref(false);
    const downloadedFilename = ref('');

    /** @param {import('@/core/types/program').Program} program */
    async function download(program) {
        if (isDownloading.value) {
            return;
        }

        isDownloading.value = true;

        try {
            const {blob, filename} = await generateWord(toGenerateRequest(program));

            saveFile(blob, filename);
            downloadedFilename.value = filename;
            toastStore.show(DOWNLOADED_MESSAGE);
        } catch (error) {
            console.error(error);
            toastStore.show(getErrorMessage(error));
        } finally {
            isDownloading.value = false;
        }
    }

    return {isDownloading, downloadedFilename, download};
}
