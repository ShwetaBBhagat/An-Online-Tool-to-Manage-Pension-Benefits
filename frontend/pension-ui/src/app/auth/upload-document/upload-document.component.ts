import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';
import { ViewChild } from '@angular/core';
import { NgForm } from '@angular/forms';

@Component({
  selector: 'app-upload-document',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterModule],
  templateUrl: './upload-document.component.html',
  styleUrls: ['./upload-document.component.css']
})
export class UploadDocumentComponent {
  selectedFile: File | null = null;
  successMsg = '';
  errorMsg = '';
  selectedDocType: string = '';

  constructor(private http: HttpClient) {}

  onFileSelected(event: any) {
    const file = event.target.files[0];

    if (file) {
      const allowedTypes = ['application/pdf', 'image/png', 'image/jpeg'];
      if (!allowedTypes.includes(file.type)) {
        this.errorMsg = 'Only PDF, PNG, JPG, JPEG files are allowed.';
        this.selectedFile = null;
      } else {
        this.selectedFile = file;
        this.errorMsg = '';
      }
    }
  }

@ViewChild('uploadForm') uploadFormRef!: NgForm;

uploadDocument() {
  const token = localStorage.getItem('userToken');

  if (!this.selectedFile) {
    this.errorMsg = 'Please select a file to upload.';
    return;
  }

  const formData = new FormData();
  formData.append('file', this.selectedFile);
  formData.append('document_type', this.selectedDocType);

  this.http.post('http://127.0.0.1:5000/api/auth/user/upload-document', formData, {
    headers: {
      Authorization: `Bearer ${token}`
    }
  }).subscribe({
    next: (res: any) => {
      this.successMsg = res.message;
      this.errorMsg = '';

      // 🧼 Reset form UI
      this.selectedFile = null;
      this.selectedDocType = '';
      const fileInput: any = document.getElementById('fileInput');
      if (fileInput) fileInput.value = '';

      // 🧼 Optionally reset Angular form
      if (this.uploadFormRef) this.uploadFormRef.resetForm();
    },
    error: (err) => {
      this.errorMsg = err.error?.error || 'Upload failed';
      this.successMsg = '';
    }
  });
}


}
