import { ComponentFixture, TestBed } from '@angular/core/testing';

import { EmployerRequestResetComponent } from './employer-request-reset.component';

describe('EmployerRequestResetComponent', () => {
  let component: EmployerRequestResetComponent;
  let fixture: ComponentFixture<EmployerRequestResetComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [EmployerRequestResetComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(EmployerRequestResetComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
