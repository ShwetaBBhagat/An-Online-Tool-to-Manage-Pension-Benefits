import { Component } from '@angular/core';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { inject, PLATFORM_ID } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';

@Component({
  selector: 'app-view-employers',
  standalone: true,
  imports: [CommonModule, HttpClientModule, RouterModule],
  templateUrl: './view-employers.component.html',
  styleUrls: ['./view-employers.component.css']
})
export class ViewEmployersComponent {
  employers: any[] = [];
  platformId = inject(PLATFORM_ID);

  constructor(private http: HttpClient) {
    this.fetchEmployers();
  }

  fetchEmployers() {
    if (!isPlatformBrowser(this.platformId)) return;
    const token = localStorage.getItem('adminToken');
    const headers = { Authorization: `Bearer ${token}` };

    this.http.get<any>('http://127.0.0.1:5000/api/admin/employers', { headers }).subscribe({
      next: (res) => {
        this.employers = res.employers || [];
      },
      error: (err) => {
        console.error('Error fetching employers:', err);
      }
    });
  }

  deleteEmployer(id: number) {
    const confirmDelete = confirm(`Are you sure you want to delete employer ID ${id}?`);
    if (!confirmDelete) return;
  
    const token = localStorage.getItem('adminToken');
    const headers = { Authorization: `Bearer ${token}` };
  
    this.http.delete(`http://127.0.0.1:5000/api/admin/employers/${id}`, { headers }).subscribe({
      next: (res: any) => {
        alert(res.message);
        this.fetchEmployers(); // Reload list
      },
      error: (err) => {
        const msg = err.error?.error || 'Error deleting employer';
        alert(`${msg}`);
      }
    });
  }  
    
}
