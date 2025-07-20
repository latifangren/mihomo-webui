#!/bin/bash

REPO_URL="https://github.com/latifangren/mihomo-webui.git"
FOLDER="mihomo-webui"

if [ -d "$FOLDER" ]; then
    echo "Folder $FOLDER sudah ada."
    echo "Pilih opsi:"
    echo "  1) Hapus dan clone ulang"
    echo "  2) Rename folder lama"
    echo "  3) Batal"
    read -p "Masukkan pilihan [1-3]: " PILIH
    PILIH="${PILIH//$'\r'/}"  # Hapus karakter carriage return jika ada
    case "$PILIH" in
        1)
            rm -rf "$FOLDER"
            git clone "$REPO_URL"
            ;;
        2)
            mv "$FOLDER" "${FOLDER}-backup-$(date +%s)"
            git clone "$REPO_URL"
            ;;
        3)
            echo "Batal."
            exit 0
            ;;
        *)
            echo "Pilihan tidak valid: '$PILIH'"
            exit 1
            ;;
    esac
else
    git clone "$REPO_URL"
fi 