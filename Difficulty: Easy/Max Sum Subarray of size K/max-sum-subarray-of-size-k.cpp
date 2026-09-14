class Solution {
  public:
    int maxSubarraySum(vector<int>& arr, int k) {
        // code here
        int n = arr.size();
        int current_sum = 0;
        
        for(int i=0; i<k; i++){
            current_sum += arr[i];
        }
        int max_sum = current_sum;
        for(int i=k; i<n; i++){
            current_sum = current_sum- arr[i-k] + arr[i];
                
            max_sum = max(current_sum, max_sum);
        }
        return max_sum;
    }
};