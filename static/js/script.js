// Dropdown functionality for project selector
document.addEventListener('DOMContentLoaded', function() {
    const projectDropdown = document.querySelector('.project-dropdown button');
  

    if (projectDropdown) {
        projectDropdown.addEventListener('click', function() {
            // This would toggle a dropdown menu in a real implementation
            console.log('Project dropdown clicked');
        });
    }
    
    // Change plan button functionality
    const changePlanBtn = document.querySelector('.change-plan-btn');
    
    if (changePlanBtn) {
        changePlanBtn.addEventListener('click', function() {
            // Scroll to pricing section
            const pricingSection = document.querySelector('.pricing-section');
            if (pricingSection) {
                pricingSection.scrollIntoView({ behavior: 'smooth' });
            }
        });
    }
    
    // Cancel subscription button
    const cancelBtn = document.querySelector('.cancel-btn');
    
    if (cancelBtn) {
        cancelBtn.addEventListener('click', function() {

            const payPalSubscriptionId = this.dataset.subscriptionId; // Get ID from data attribute
        
            if (!payPalSubscriptionId) {
                alert('Error: Subscription ID not found. Cannot cancel.');
                return;
            }

            if (confirm('Are you sure you want to cancel your subscription?')) {
                console.log('Initiating cancellation for PayPal Subscription ID:', payPalSubscriptionId);


                // This would handle the PayPal cancellation in a real implementation #ak47
                
                fetch(cancelURL, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json', // Sending JSON
                        'X-CSRFToken': csrfToken,
                    },
                    body: JSON.stringify({
                        paypal_subscription_id: payPalSubscriptionId,
                        reason: 'User requested cancellation via website.' // Optional reason
                    })
                }).then(response => {
                    if (response.ok) {
                        return response.json();
                    } else {
                    // Try to get error message from server response if JSON
                    return response.json().then(errData => {
                        throw new Error(errData.error || `Server error: ${response.status}`);
                    }).catch(() => {
                        // Fallback if response isn't JSON or doesn't have .error
                        throw new Error(`Failed to cancel subscription. Server responded with ${response.status}`);
                    });
                }
                }).then(data => {
                    if (data.success) {
                        alert('Subscription cancelled successfully!');
                        window.location.reload(); // Or redirect to a confirmation page
                    } else {
                        alert('Failed to cancel subscription: ' + (data.error || 'Unknown error from server.'));
                    }
                }).catch(function (err) {
                    // Hide loading indicator
                    console.error("Cancellation request failed:", err);
                    alert("An error occurred while trying to cancel your subscription: " + err.message);
                });
                // This would handle the PayPal cancellation in a real implementation #ak47

                // This would handle subscription cancellation in a real implementation
            }
        });
    }
    
    // Choose plan buttons
    const choosePlanBtns = document.querySelectorAll('.choose-btn');
    
    if (choosePlanBtns) {
        choosePlanBtns.forEach(btn => {
            btn.addEventListener('click', function() {
                const planName = this.closest('.pricing-card').querySelector('h3').textContent;
                console.log(`Switching to ${planName}`);
                // This would handle plan switching in a real implementation
                


            console.log(`${currentSubscriptionId} You're about to change your current plan. Continue?",${selectedPlanId}, ${currentPlanId}`);
            selectedPlanId = this.getAttribute('data-plan-id');

            // If user already has a subscription, update it
            if (currentSubscriptionId  && selectedPlanId !== currentPlanId) {
                if (!confirm("You're about to change your current plan. Continue?")) return;

                fetch(updateUrl, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrfToken
                    },
                    body: JSON.stringify({
                        subscription_id: currentSubscriptionId,
                        new_plan_id: selectedPlanId
                    })
                }).then(response => response.json())
                  .then(result => {
                      if (result.success) {
                          alert("Plan changed successfully!");
                          window.location.reload();
                      } else {
                          alert("Failed to change plan: " + result.error);
                      }
                  });
                return;
            }

            // Else, render PayPal button for new subscription            
            document.getElementById('paypal-button-container').innerHTML = '';
            paypal.Buttons({
                createSubscription: function (data, actions) {
                    return actions.subscription.create({
                        plan_id: selectedPlanId
                    });
                },
                onApprove: function (data) {
                    fetch(saveUrl, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': csrfToken
                        },
                        body: JSON.stringify({
                            subscriptionID: data.subscriptionID,
                            planID: selectedPlanId
                        })
                    }).then(response => response.json())
                      .then(result => {
                          if (result.success) {
                              window.location.reload();
                          } else {
                              alert('Subscription failed: ' + result.error);
                          }
                      });
                }
            }).render('#paypal-button-container');



                // Show a confirmation message
                alert(`You have selected the ${planName}. This change will take effect on your next billing cycle.`);
            });
        });
    }
    
    // Sidebar navigation highlighting
    const sidebarLinks = document.querySelectorAll('.sidebar-nav a');
    
    if (sidebarLinks) {
        sidebarLinks.forEach(link => {
            link.addEventListener('click', function(e) {
                // Remove active class from all links
                sidebarLinks.forEach(l => l.parentElement.classList.remove('active'));
                
                // Add active class to clicked link
                this.parentElement.classList.add('active');
            });
        });
    }
});