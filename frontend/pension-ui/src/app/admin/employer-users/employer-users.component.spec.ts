import { ComponentFixture, TestBed } from '@angular/core/testing';

import { EmployerUsersComponent } from './employer-users.component';

describe('EmployerUsersComponent', () => {
  let component: EmployerUsersComponent;
  let fixture: ComponentFixture<EmployerUsersComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [EmployerUsersComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(EmployerUsersComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
