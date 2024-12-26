import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ConsulterDpiComponent } from './consulter-dpi.component';

describe('ConsulterDpiComponent', () => {
  let component: ConsulterDpiComponent;
  let fixture: ComponentFixture<ConsulterDpiComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ConsulterDpiComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ConsulterDpiComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
